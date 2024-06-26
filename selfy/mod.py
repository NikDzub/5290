#!/usr/bin/env python3
import random
import os
import shutil

# basic

url = "https://www.tiktok.com/"


def split_list(li, segments):
    segment_size = len(li) // segments
    remainder = len(li) % segments
    segments_list = []
    start = 0
    for i in range(segments):
        if i < remainder:
            end = start + segment_size + 1
        else:
            end = start + segment_size
        segments_list.append(li[start:end])
        start = end
    return segments_list


# search


def get_users1(segments):
    # with open("./etc/username_list.txt") as f:
    with open("../etc/new_user_list.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        top_users = []
        with open("../etc/top_users.txt") as f:
            for line in f.readlines():
                top_users.append(line.replace("\n", ""))
        random.shuffle(top_users)

        top_users = top_users[:5]
        for top in top_users:
            username_list.insert(0, top)
        return split_list(username_list, segments)


def get_users_il():

    with open("../etc/israel_usrs.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        return username_list


def get_users(segments):
    # with open("./etc/username_list.txt") as f:
    with open("../etc/new_user_list.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        top_users = []
        with open("../etc/top_users.txt") as f:
            for line in f.readlines():
                top_users.append(line.replace("\n", ""))
        random.shuffle(top_users)

        top_users = top_users[:5]
        for top in top_users:
            username_list.insert(0, top)

        return username_list


def get_reply():
    with open("./etc/replies.txt") as f:
        replies = []
        for line in f.readlines():
            replies.append(line.replace("\n", ""))

        random.shuffle(replies)
        return replies


def get_used_vids():
    with open("./etc/used_videos.txt", "r") as file:
        used_vids = []
        lines = file.readlines()
        for line in lines:
            used_vids.append(line.replace("\n", ""))
        return used_vids


def clean_firefox():
    context_dir = "./firefox"
    context_dir = os.path.join(os.getcwd(), context_dir)
    try:
        shutil.rmtree(f"{context_dir}/sessionstore-backups")
        os.remove(f"{context_dir}/sessionCheckpoints.json")
        os.remove(f"{context_dir}/sessionstore.jsonlz4")
    except Exception as error:
        pass
        # print(error)


def clean_local_firefox():
    context_dir = "/Users/ihpt/Library/Application Support/Firefox/Profiles/i8unqabt.default-nightly"
    context_dir = os.path.join(os.getcwd(), context_dir)
    try:
        shutil.rmtree(f"{context_dir}/storage")
        shutil.rmtree(f"{context_dir}/crashes")
        shutil.rmtree(f"{context_dir}/sessionstore-backups")
        os.remove(f"{context_dir}/sessionCheckpoints.json")
        os.remove(f"{context_dir}/sessionstore.jsonlz4")
    except Exception as error:
        pass
        # print(error)


class Video:
    def __init__(
        self,
        creator,
        verified,
        vid_id,
        hr_ago,
        comments,
        likes,
        plays,
        bookmarks,
        shares,
    ):
        self.creator = creator
        self.verified = verified
        self.vid_id = vid_id
        self.hr_ago = hr_ago
        self.comments = comments
        self.likes = likes
        self.plays = plays
        self.bookmarks = bookmarks
        self.shares = shares

    def display_info(self):
        print(
            f"\n{url}@{self.creator}/video/{self.vid_id} \nhr_ago: {int(self.hr_ago)} comments: {self.comments} likes: {self.likes:,} plays: {self.plays:,} bookmarks: {self.bookmarks:,} shares: {self.shares:,}"
        )

    def video_url(self):
        # print(f"{url}@{self.creator}/video/{self.vid_id}")
        return f"{url}@{self.creator}/video/{self.vid_id}"

    def valid(self):
        if (
            (self.likes / (self.hr_ago * 1000) > 0.5)
            and (self.hr_ago < 2)
            and (self.comments > 90)
            and (self.comments < 200)
        ):
            return True


# emu

app_name = "com.zhiliaoapp.musically"
# app_name = "com.zhiliaoapp.musically.go"
lock = "com.android.systemui:id/lock_icon"


pause = "com.zhiliaoapp.musically:id/arr"
comments = "com.zhiliaoapp.musically:id/bw1"
actual_comment = "com.zhiliaoapp.musically:id/c6c"


# likes


def get_new_vids():
    new_videos = []
    with open("./new_videos.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            new_videos.append(line.replace("\n", ""))
    return new_videos


def get_cookies(like_browsers):
    if os.path.exists("../etc/cookies/.DS_Store"):
        os.remove("../etc/cookies/.DS_Store")
    cookies_json = os.listdir("../etc/cookies")
    random.shuffle(cookies_json)
    return split_list(cookies_json[:15], like_browsers)
