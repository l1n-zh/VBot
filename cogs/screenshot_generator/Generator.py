from html2image import Html2Image
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = 'localhost'
PORT = 33333
server_addr = (HOST, PORT)

def parse(message:str) -> str:
    s.sendto(message.encode(), server_addr)
    result, _ = s.recvfrom(33333)
    return result.decode()

class Generator:
    def __init__(self, img_id):
        self.img_id = img_id
        self.html = ""
        self.height = 0

    def add(self, name, color, avatar_url, message, time):
        self.height += (message.count("\n")*50 or 50) + 130
        if not color.value : color = "white"
        message = parse(message)
        self.html += (
            f"""<div class="discord">
                <img src="{avatar_url}"
                    class="avatar" />
                <div class="content">
                    <span class="name" style="color:{color}">{name}</span>
                    <span class="time">{time}</span>
                        <div class="message">
                            {message}
                        </div>
                </div>
            </div>""")


    def generate(self):
        hti = Html2Image(size=(1200, self.height), output_path="./buffer")
        with open("cogs/screenshot_generator/style.css") as stylesheet:
            hti.screenshot(html_str=self.html, css_str=stylesheet, save_as = f"screenshot{self.img_id}.png")