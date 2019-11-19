import os
from datetime import date, datetime
import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer

# Initialize a new API instance and get an access key
api = landsatxplore.api.API("remoteSensingErsl", "ErslRemoteSensing00")

# Request
# Images before 1984
scenes_early = api.search(
    dataset='LANDSAT_MSS_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1981-01-01',
    end_date='1983-12-31',
    max_cloud_cover=10,
    max_results=1000)

# Images after 1984
scenes = api.search(
    dataset='LANDSAT_TM_C1',
    bbox=(51.1931, 11.2830, 53.5990, 14.8865),
    start_date='1984-01-01',
    end_date='1995-12-31',
    max_cloud_cover=10,
    max_results=1000)

today = date.today()
datemin = datetime.strptime("06-01", "%m-%d").date().replace(year=today.year)
datemax = datetime.strptime("07-31", "%m-%d").date().replace(year=today.year)
selected_scenes = []

# LANDSAT_MSS_C1 does not download

#for scene in scenes_early:
#    time = scene['acquisitionDate']
#    if time[-5:] != "02-29":
#        scenedate = datetime.strptime(time, '%Y-%m-%d').date().replace(year=today.year)
#
#        if datemin < scenedate < datemax:
#            selected_scenes.append(scene)

for scene in scenes:
    time = scene['acquisitionDate']
    if time[-5:] != "02-29":
        scenedate = datetime.strptime(time, '%Y-%m-%d').date().replace(year=today.year)

        if datemin < scenedate < datemax:
            selected_scenes.append(scene)

print('{} scenes found.'.format(len(selected_scenes)))

api.logout()

# Start downloading
ee = EarthExplorer("remoteSensingErsl", "ErslRemoteSensing00")

current_directory = os.getcwd()

# Creating the "images" directory
if not os.path.isdir(current_directory + '/images'):
    os.mkdir(current_directory + '/images')
else:
    print("Directory 'images' already exists")

for scene in selected_scenes:
    year = scene['acquisitionDate'][:4]
    scene_id = scene['entityId']
    display_id = scene['displayId']
    if not os.path.isdir(current_directory + '/images/' + year):
        os.mkdir(current_directory + '/images/' + year)
    else:
        print("Directory for " + year + " already exists")
    if not os.path.isfile(current_directory + '/images/' + year + '/' + display_id + '.tar.gz'):
        try:
            ee.download(scene_id=scene_id, output_dir=current_directory + '/images/' + year)
        except Exception as err:
            print("An Error has occurred:")
            print(err)
    else:
        print("File " + display_id + " already exists")

ee.logout()
