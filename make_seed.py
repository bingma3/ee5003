import libtorrent as lt


def make_seed():
    fs = lt.file_storage()
    lt.add_files(fs, "./video_repo/temp_1.mp4")
    t = lt.create_torrent(fs)
    t.add_tracker("http://192.168.1.85/")
    t.add_url_seed("http://192.168.1.85/")
    t.add_http_seed("http://192.168.1.85/")
    t.set_creator("smartooh torrent")
    t.set_comment("smartooh video")
    t.set_priv(True)
    lt.set_piece_hashes(t, "./video_repo")
    with open("./video_repo/video.torrent", "wb") as f:
        f.write(lt.bencode(t.generate()))


if __name__ == "__main__":
    make_seed()
