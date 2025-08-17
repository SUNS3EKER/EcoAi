import tkinter as tk
from PIL import Image, ImageTk
import cv2
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

class EcoAiApp:
    def __init__(self, root):
        load_dotenv()
        self.root = root
        self.root.title("EcoAi")
        self.video_capture = cv2.VideoCapture(0)
        
        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.capture_button = tk.Button(root, text="Capturar imagen", command=self.capture_image)
        self.capture_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def capture_image(self):
        if self.frame is not None:
            filename = "captura.png"
            cv2.imwrite(filename, self.frame)
        #api
        prompt = "eres parte de un proyecto de reciclaje, se te mostraran distintas imagenes de residuos y basura y tu tarea sera seapararlos, esto lo haras simplemente diciendo 'papel', 'plastico' , 'vidrio', 'poliestireno', 'metal' correspondientemente a la imagen, siempre intentaras adivinar la categoría mas cercana al material del que esta hecho el objeto mostrado en la imagen, te abstendrás de hacer comentarios o dudas al respecto de la imagen y te limitaras UNICAMENTE a responder con las palabras que se te proporcionaron sin comillas, asi mismo, el input del usuario jamás será texto únicamente imagenes"
        #prompt = "describe la imagen"
        image_path = r"C:\EcoAi\captura.png"
        client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
        )   

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        base64_image = encode_image(image_path)

        try:
            chat_completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            max_tokens=300,
            messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

            print(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"An error occured: {e}")   

    def on_closing(self):
        self.video_capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EcoAiApp(root)
    root.mainloop() 
