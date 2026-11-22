package com.npmartinez.shoplist;

import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;
import org.json.JSONObject;

// Recipe links shared from Chrome (Share -> Shopping List) are handed to the page's onShared().
public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        handleShare(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        handleShare(intent);
    }

    private void handleShare(Intent intent) {
        if (intent == null || !Intent.ACTION_SEND.equals(intent.getAction())) return;
        String text = intent.getStringExtra(Intent.EXTRA_TEXT);
        if (text == null || getBridge() == null) return;
        final WebView wv = getBridge().getWebView();
        final String js = "(typeof window.onShared==='function'&&window.appReady)?(onShared(" + JSONObject.quote(text) + "),'ok'):'wait'";
        wv.post(new Runnable() {
            int tries = 0;
            @Override public void run() {
                wv.evaluateJavascript(js, v -> {
                    if (!"\"ok\"".equals(v) && tries++ < 60) wv.postDelayed(this, 250);
                });
            }
        });
    }
}
