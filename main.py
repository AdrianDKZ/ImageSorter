import exifread, os
from shutil import copyfile

DIR_INIT = "testing/images/"        # Initial directory of the images to be sorted
DIR_GOAL = "testing/goal/"          # Goal directory of the images to be sorted
DIR_FAIL = "testing/fail/"          # Fail directory to store the images w/o date time
DIR_GOAL_REP = "testing/repeated/"  # Directory where store the repeated images from the goal directory

#Return the date when the image was taken. In casa data is not available, return "None"
def getImageDate(image):
    with open(image, 'rb') as img:
        try:
            return exifread.process_file(img)["Image DateTime"].values.split(" ")[0].split(":")[:-1]
        except KeyError:
            print("Image date time not found")

#Check if the goal path exists and, if not, create the needed folders
def checkPath(path, subfolder):
    path = path + subfolder + "/"
    if os.path.exists(path) is False:
        os.mkdir(path)
    return path

#Return the path where the image must be stored
def getGoalPath(image_name,image_date):
    goalPath = ""
    if image_date is None:
        goalPath = DIR_FAIL + image_name
    else:
        goalPath = checkPath(checkPath(DIR_GOAL, image_date[0]), image_date[1]) + image_name
        if os.path.exists(goalPath) is True:
            goalPath = DIR_GOAL_REP + image_name
    return goalPath

def main():
    for image_name in os.listdir(DIR_INIT):
        image_path = os.path.join(DIR_INIT,image_name)
        if os.path.isfile(image_path):
            copyfile(image_path,getGoalPath(image_name,getImageDate(image_path)))

if __name__ == "__main__":
    main()
