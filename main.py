import logging
import pyperclip
import subprocess
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

logger = logging.getLogger(__name__)

class KeystoreExtension(Extension):

    def __init__(self):
        super(KeystoreExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        
        # Get all keys from the keystore
        try:
            keys = self.get_keystore_keys()
            
            # Filter keys based on the query
            if query:
                filtered_keys = [key for key in keys if query.lower() in key.lower()]
            else:
                filtered_keys = keys
            
            # Create result items for each key
            items = []
            for key in filtered_keys[:8]:  # Limit to 8 results for better UI
                items.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=key,
                        description=f"Copy value of '{key}' to clipboard",
                        on_enter=CopyToClipboardAction(self.get_keystore_value(key))
                    )
                )
            
            if not items:
                items.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name="No matching keys found",
                        description="Try a different search term",
                        on_enter=CopyToClipboardAction("")
                    )
                )
                
            return RenderResultListAction(items)
            
        except Exception as e:
            logger.error(f"Error accessing keystore: {e}")
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name="Error accessing keystore",
                    description=str(e),
                    on_enter=CopyToClipboardAction("")
                )
            ])
    
    def get_keystore_keys(self):
        """Get all keys from the keystore using slpd list command"""
        result = subprocess.run(['slpd', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to list keys: {result.stderr}")
        
        # Parse the output to get the keys
        keys = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return keys
    
    def get_keystore_value(self, key):
        """Get the value for a specific key using slpd get command"""
        result = subprocess.run(['slpd', 'get', key], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to get value for key '{key}': {result.stderr}")
        
        return result.stdout.strip()

if __name__ == '__main__':
    KeystoreExtension().run()
