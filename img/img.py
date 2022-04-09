import glob
from PIL import Image
def make_gif(frame_folder):
    #frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    frames = []
    for img in range(1,22):
        tmp_frame = Image.open("./gif/{}.png".format(img))
        frames.append(tmp_frame)

    frame_one = frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
               save_all=True, duration=600, loop=0)
    
if __name__ == "__main__":
    make_gif("./gif")