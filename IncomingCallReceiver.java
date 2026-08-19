package com.hackathon.scamshield;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.telephony.TelephonyManager;
import android.widget.Toast;

public class IncomingCallReceiver extends BroadcastReceiver {
    
    // Sample offline database of high-risk reported numbers
    private static final String[] SPAM_NUMBERS = {"+18005550199", "+919876543210"};

    @Override
    public void onReceive(Context context, Intent intent) {
        String state = intent.getStringExtra(TelephonyManager.EXTRA_STATE);

        // Triggers instantly when the device starts RINGING
        if (TelephonyManager.EXTRA_STATE_RINGING.equals(state)) {
            String incomingNumber = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER);
            
            if (incomingNumber != null) {
                boolean isSpam = checkIsSpam(incomingNumber);
                
                if (isSpam) {
                    // Display system-level pop-up notification over the call screen
                    Toast.makeText(context, "🚨 ALERT: High Risk Scam Call from " + incomingNumber, Toast.LENGTH_LONG).show();
                    // Here you can trigger a custom HUD Overlay Activity or ring-tone mute
                }
            }
        }
    }

    private boolean checkIsSpam(String number) {
        for (String spamNum : SPAM_NUMBERS) {
            if (spamNum.equals(number)) return true;
        }
        return false;
    }
}
