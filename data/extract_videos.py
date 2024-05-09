import pandas as pd
import os, cv2
from multiprocessing import Pool
import numpy as np


def extract_videos():
    in_video_dir = 'downloaded_videos/'
    out_video_dir = 'extracted_videos/'
    os.makedirs(out_video_dir, exist_ok=True)

    df = pd.read_pickle('golfDB.pkl')

    for idx in range(len(df.id)):
        print(f'Progress {idx+1}/{len(df.id)}...')

        anno_id = df.id[idx]
        bbox = df.bbox[idx]
        events = df.events[idx]
        youtube_id = df.youtube_id[idx]

        in_video_mp4 = os.path.join(in_video_dir, "{}.mp4".format(youtube_id))
        in_video_mkv = os.path.join(in_video_dir, "{}.mp4".format(youtube_id))
        in_video_webm = os.path.join(in_video_dir, "{}.webm".format(youtube_id))
        out_video_file = os.path.join(out_video_dir, "{:06d}.mp4".format(anno_id))

        if not os.path.isfile(out_video_file):
            print('Processing annotation id {}'.format(anno_id))

            cap = None
            for ext in ['mp4', 'mkv', 'webm']:
                in_video_file = os.path.join(in_video_dir, "{}.{}".format(youtube_id, ext))
                if os.path.isfile(in_video_file):
                    cap = cv2.VideoCapture(in_video_file)
            
            if cap is None:
                print(f'Not found valid video for id: {anno_id} - {youtube_id}')
                continue
            
            x = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * bbox[0])
            y = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * bbox[1])
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * bbox[2])
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * bbox[3])

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(out_video_file, fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))

            out_image_dir = os.path.join(out_video_dir, "{:06d}_events".format(anno_id))
            os.makedirs(out_image_dir, exist_ok=True)

            count = 0
            success, image = cap.read()
            while success:
                count += 1
                if count >= events[0] and count <= events[-1]:
                    crop_img = image[y:y + h, x:x + w]
                    out.write(crop_img)
                    if count in events:
                        eidx = list(events).index(count)
                        out_image_file = os.path.join(out_image_dir, f'event_{eidx:03d}.jpg')
                        cv2.imwrite(out_image_file, crop_img)
                if count > events[-1]:
                    break
                success, image = cap.read()

            cap.release()
            out.release()

        else:
            print('Annotation id {} already completed.'.format(anno_id))


if __name__ == '__main__':
    extract_videos()

