"""
Possible solutions to in-class practice exercises
Lesson 10.2
about harvesting comments from Youtube videos
"""
# Using your API key, harvest 100 comments from a Youtube video of your choice and
# save the JSON object to a .json file on your hard drive. If you don't know which
# video to choose, why not use this one here from Dude Perfect.
from googleapiclient.discovery import build
import json

def get_comments(response):
    comments = []
    for comment in response['items']:
        comments.append(comment['snippet']['topLevelComment']["snippet"]['textOriginal'])
    return comments

if __name__ == '__main__':
    # NEVER ACTUALLY DO THIS IN ANY OTHER PROGRAM!!!
    api_key = "AIzaSyCEDW3a-YLDoE0D6Qn5CKZ2Nm9N_C1Xs24"

    # This is fine
    video_id = "ZZ5LpwO-An4" # Heyayayayay video

    # creating Google API class for YouTube
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.commentThreads().list(
            part="snippet",
            maxResults="100",
            videoId=video_id,
            textFormat="plainText"
            )
    response = request.execute()

    # Initializing the list, comments, to use for further comment fetching
    comments = get_comments(response)

    # Get the page token for the next page
    nextPage = response["nextPageToken"]
    for i in range(5):
        # Create a new comment thread request based on the nextPage token
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults="100",
            videoId=video_id,
            textFormat="plainText",
            pageToken=nextPage
        )
        response = request.execute()
        comments += get_comments(response)
        nextPage = response["nextPageToken"]


    print(len(comments))
    comments_dict = { 'comments' : comments }

    # Write all the comments to a file
    with open(f"youtube_comments_{video_id}.json", "w") as outfile:
        json.dump(comments_dict, outfile)


