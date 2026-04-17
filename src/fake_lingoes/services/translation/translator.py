# -*- coding: utf-8 -*-

import mtranslate
from googletrans import Translator


# Translate_ return a string
def googleTrans(myText, fromLang='en', toLang='vi'):
    try:
        # mtranslate is usually more reliable for synchronous calls in this environment
        outText = mtranslate.translate(myText, to_language=toLang, from_language=fromLang)
        if outText and not outText.startswith("Lỗi!!!"):
            return outText
    except Exception as e:
        print(f"mtranslate error: {e}")

    try:
        myTransTool = Translator()
        # In version 4.0.x, translate() might be async. 
        # Since this is a synchronous context, we check if it returns a coroutine.
        myTrans = myTransTool.translate(myText, src=fromLang, dest=toLang)
        
        # If it's a coroutine, we can't easily wait for it here without an event loop.
        # So we just return the error string and let it fall back or show the error.
        if hasattr(myTrans, 'text'):
            return str(myTrans.text)
        else:
            return "Lỗi!!! Không thể dịch được (Async mismatch)"
    except Exception as e:
        print(f"googletrans error: {e}")
    
    return "Lỗi!!! Không thể dịch được"

