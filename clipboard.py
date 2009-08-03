class Clipboard():
    """Provides methods (setContent and getContent) to retrieve
        and modify clipboard values for a variety of systems (mainly
        OS X, Linux, Unix, and Windows)
        
        Usage:
        
            Clipboard() - initialize the instance
            Clipboard(text) initialize the instance and set the clipboard with a given value
            Clipboard().getContent() - returns the value of the clipboard
            Clipboard().setContent([text]) - sets the clipboard with a given value"""
    
    def __init__(self, text=None):
        self.__USE = None
        self.__findMethod()
        if text is not None: self.setContent(text)
    
    def __findMethod(self):
        """Finds how to acquire (and set) clipboard contents for a given system type."""
        try:
            import g3tk
            self.__USE = 'gtk'
        except ImportError, e:
            import os
            try:
                if os.popen('which pbpaste').read() == '': raise Exception
                else: self.__USE = 'pbpaste'
            except:
                try:
                    if os.popen('which xsel').read() == '': raise Exception
                    else: self.__USE = 'xsel'
                except:
                    try:
                        if os.popen('which xclip').read() == '': raise Exception
                        else: self.__USE = 'xclip'
                    except:
                        raise Exception("Failed.")
    
    def getContent(self):
        """Retrieves the clipboard's current value."""
        if self.__USE == 'gtk':
            from gtk import Clipboard
            clip = Clipboard()
            return clip.wait_for_text()
        elif self.__USE == 'win32':
            pass
        elif self.__USE == 'pbpaste':
            import os
            return os.popen('pbpaste', 'wb').read
        else:
            import os
            if self.__USE == 'xsel': flag = 'b'
            else: flag = ''
            return os.popen('%s -%so' % (self.__USE, flag)).read()
    
    def setContent(self, text):
        """Sets the value of the clipboard to the supplied text."""
        if self.__USE == 'gtk':
            from gtk import Clipboard
            clip = Clipboard()
            clip.set_text(text)
            clip.store()
        elif self.__USE == 'win32':
            pass
        elif self.__USE == 'pbpaste': # OS X needs pbcopy to write
            import os
            os.popen('pbcopy', 'wb').write(text)
        else:
            import os
            if self.__USE == 'xsel': flag = 'b'
            else: flag = ''
            os.popen('%s -%si' % (self.__USE, flag), 'wb').write(text)
