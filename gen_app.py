import pathlib, shutil
def w(p, s):
    f = pathlib.Path(p); f.parent.mkdir(parents=True, exist_ok=True); f.write_text(s, encoding='utf-8')

w('settings.gradle', r'''pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositories { google(); mavenCentral() } }
rootProject.name = 'Ledger'
include ':app'
''')
w('build.gradle', r'''plugins { id 'com.android.application' version '8.5.2' apply false }
''')
w('gradle.properties', r'''org.gradle.jvmargs=-Xmx3g
android.useAndroidX=false
''')
w('app/build.gradle', r'''plugins { id 'com.android.application' }
android {
    namespace 'com.ledger.app'
    compileSdk 34
    defaultConfig {
        applicationId 'com.ledger.app'
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName '1.0'
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
''')
w('app/src/main/AndroidManifest.xml', r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:label="记账" android:allowBackup="true"
        android:theme="@android:style/Theme.DeviceDefault.Light.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true"
            android:windowSoftInputMode="adjustResize"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
''')
w('app/src/main/java/com/ledger/app/MainActivity.java', r'''package com.ledger.app;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#eef1f4"));
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        web.loadUrl("file:///android_asset/index.html");
        setContentView(web);
    }

    @Override
    public void onBackPressed() {
        web.evaluateJavascript("(window.goBack&&window.goBack())?'1':'0'", v -> { if (!"\"1\"".equals(v)) finish(); });
    }

    @Override
    protected void onPause() { super.onPause(); web.onPause(); }

    @Override
    protected void onResume() { super.onResume(); web.onResume(); }
}
''')
pathlib.Path('app/src/main/assets').mkdir(parents=True, exist_ok=True)
shutil.copy('index.html', 'app/src/main/assets/index.html')
