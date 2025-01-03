from gui.gui_manager import GUIManager

def main():
    app = GUIManager()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Cos sie zepsulo w mainie :( ", e)
