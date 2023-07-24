# Custom JavaScript events for OBS Studio browser sources <br> OBS 浏览器源自定义 JS 事件

[简体中文 · Read in Simplified Chinese](README-zh.md)

This Python script for OBS Studio allows you to trigger custom JavaScript events on all browser sources (in the current scene collection) using hotkeys.

## Usage

 1. Launch OBS Studio. Under **Tools > Scripts**, open the **Python Settings** tab. Choose the installation folder of Python. Make sure you have Python installed and it has the same architecture as OBS studio (e.g. for 64-bit OBS Studio install 64-bit Python, not 32-bit Python).

    ![Browse to the correct path using the “Python Install Path” box in “Python Settings”. It will tell you your OBS Studio architecture. Once the correct path is selected, you should see the line “Loaded Python Version: 3.xx”.](images/1.png)

 2. In the same window, navigate back to the **Scripts** tab and click on the plus button in the bottom left. Choose the `custom-browser-events.py` file.

    ![The plus button says “Add Scripts” when hovered.](images/2.png)

 3. After the script is loaded, you should see the **Events** box to the right. Here you can manage your custom events.

    ![A description of the script and the “Events” box show up in the right side of the window. There are three default events, “obsCustomEvent1” through “obsCustomEvent3”.](images/3.png)

 4. Once you are happy with the event names, you can close the **Scripts** window and go to **Files > Settings > Hotkeys** to set your hotkeys. The custom events will appear at the bottom of the topmost section, above the sections for specific scenes.

    ![You will see new available actions labeled “Custom browser event” followed by your event names.](images/4.png)

 5. To listen for custom events, simply add something like this in the JavaScript code for your browser page:

    ~~~js
    window.addEventListener("obsCustomEvent1", function (ev) {
      document.body.append("Hello, world!")
    })
    ~~~

    Or with a function declaration:

    ~~~js
    function doSomething(ev) {
      // ...
    }
    window.addEventListener("obsCustomEvent1", doSomething)
    ~~~

    Omit “`window.`” if you like.
