import json
import os

def readDataFrom(filename):
    with open(filename, 'r') as f:
        return f.read()

def getMedia(item):

    def getUserTags(item):
        usertags = item['usertags']['in'] if item['usertags'] is not None else []
        return [ usertag['user'] if usertag is not None else None for usertag in usertags ]
    
    def getFeed(item):
        return item['image_versions2']['candidates'][0]['url']
    
    def getClip(item):
        return item['video_versions'][0]['url'] 
    
    def getAudio(item):
        audio_info = {}
        if item['has_audio'] and item['clips_metadata'] is not None:
            if item['clips_metadata']['audio_type'] == 'licensed_music':
                
                audio_info['audio_type'] = 'licensed_music'
                
                music_asset_info = item['clips_metadata']['music_info']['music_asset_info']
                audio_info['title'] = music_asset_info['title']
                audio_info['artist'] = music_asset_info['display_artist']

            else:
                audio_info['audio_type'] = 'original'

        return audio_info
    
    if item['product_type'] == 'clips' or item['product_type'] == 'igtv':
        return {
            "usertags" : getUserTags(item),
            "audio": getAudio(item),
            "url" : getClip(item)
        }
    elif  item['product_type'] == 'feed':
        return {
            "usertags" : getUserTags(item),
            "audio": getAudio(item),
            "url" : getFeed(item)
        }
    elif item['product_type'] == 'carousel_container': 
        media = []
        for carousel_item in item['carousel_media']:
                if carousel_item['media_type'] == 1:
                    media.append({
                        "usertags" : getUserTags(carousel_item),
                        "accessibility_caption" : carousel_item['accessibility_caption'],
                        "product_type" : "feed",
                        "url": getFeed(carousel_item)
                    })
                elif  item['media_type'] == 2:
                    media.append({
                        "usertags" : getUserTags(carousel_item),
                        "accessibility_caption" : carousel_item['accessibility_caption'],
                        "product_type": "clips",
                        "url": getClip(carousel_item)
                    })
        return media
    else :
        print("Unknow Media Type Detected")
        saveAsJson(item, 'debug.json')
        return {}
    
def saveAsJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def processUserDetails(userInfo):
    
    userInfo['profile_pic_url'] = userInfo['hd_profile_pic_url_info']['url']
    
    del userInfo['hd_profile_pic_url_info']
    del userInfo['friendship_status']
    del userInfo['is_embeds_disabled']
    del userInfo['is_unpublished']
    del userInfo['latest_besties_reel_media']
    del userInfo['latest_reel_media']
    del userInfo['live_broadcast_visibility']
    del userInfo['live_broadcast_id']
    del userInfo['seen']
    del userInfo['supervision_info']
    del userInfo['__typename']
    
    return userInfo

def setIfPresent(item, key, value):
    if value is not None:
        return {**item, key: value}
    return item

def processPostInfo(postInfo):

    post = setIfPresent({}      ,'code'                    , postInfo['code'])
    post = setIfPresent(post    ,'pk'                      , postInfo['pk'])
    post = setIfPresent(post    ,'id'                      , postInfo['id'])
    post = setIfPresent(post    ,'caption'                 , postInfo['caption']['text'] if postInfo['caption'] is not None else postInfo['caption'])
    post = setIfPresent(post    ,'accessibility_caption'   , postInfo['accessibility_caption'])
    post = setIfPresent(post    ,'added_at'                , postInfo['taken_at'])
    post = setIfPresent(post    ,'like_count'              , postInfo['like_count'])
    post = setIfPresent(post    ,'comment_count'           , postInfo['comment_count'])
    post = setIfPresent(post    ,'product_type'            , postInfo['product_type'])
    post = setIfPresent(post    ,'media'                   , getMedia(postInfo))
    post = setIfPresent(post    ,'location'                , postInfo['location'])

    return post


if __name__ == '__main__':

    raw_data_path='./data/raw/'
    raw_files = [ f for f in os.listdir(raw_data_path) 
            if os.path.isfile(os.path.join(raw_data_path, f)) ]
    
    # raw_files = ['blokewithabind.json']
    
    for raw_file in raw_files:
        
        content = readDataFrom(f'{raw_data_path}/{raw_file}')
        content = json.loads(content)

        data = {
            "user" : processUserDetails(content[0]['node']['user']),
            "posts": []
        }

        data['posts'] = [ processPostInfo(item['node']) for item in content ]

        saveAsJson(data, f'./data/processed/{raw_file}')

        # timeline = [ { 
        #             "epoch": p['added_at'], 
        #             "caption": p['caption'] 
        #             } 
        #             if p.get('caption', None) is not None else {} 
        #             for p in data['posts'] ]
        
        # saveAsJson(timeline, 'timeline.json')

