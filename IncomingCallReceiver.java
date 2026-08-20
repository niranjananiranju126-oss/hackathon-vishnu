package com.scamshield.ai;

import android.telecom.Call;
import android.telecom.CallScreeningService;
import android.util.Log;

public class IncomingCallReceiver extends CallScreeningService {

    private static final String TAG = "ScamShieldAI";

    // Known malicious numbers for testing (Can be fetched dynamically from app.py / API)
    private static final String[] BLACKLIST = {"+18005550199", "+18001234567"};

    @Override
    public void onScreenCall(Call.Details callDetails) {
        if (callDetails.getCallDirection() == Call.Details.DIRECTION_INCOMING) {
            
            // Extract the incoming phone number
            String incomingNumber = callDetails.getHandle().getSchemeSpecificPart();
            Log.d(TAG, "Incoming call detected from: " + incomingNumber);

            // Check if incoming number is blacklisted
            if (isBlacklisted(incomingNumber)) {
                Log.w(TAG, "BLOCKED SPAM CALL: " + incomingNumber);

                // Build a response that rejects the call before the phone rings
                CallResponse response = new CallResponse.Builder()
                        .setDisallowCall(true)        // Block call
                        .setRejectCall(true)          // Decline incoming ring
                        .setSkipNotification(false)   // Show "Blocked by ScamShield" alert
                        .build();

                respondToCall(callDetails, response);
            } else {
                // Allow safe calls to pass through normally
                Log.i(TAG, "PASSED SAFE CALL: " + incomingNumber);
                respondToCall(callDetails, new CallResponse.Builder().build());
            }
        }
    }

    private boolean isBlacklisted(String number) {
        for (String spamNumber : BLACKLIST) {
            if (number.contains(spamNumber)) {
                return true;
            }
        }
        return false;
    }
}
