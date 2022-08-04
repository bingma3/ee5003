import libtorrent as lt
import time
<<<<<<< HEAD
import sys
=======
import datetime
import schedule
>>>>>>> 17e3fbdbd5ad861773809d00125aa72201e2736c

ses = lt.session()
with open("./video_repo/video.torrent", 'rb') as f:
    torrent = lt.bdecode(f.read())

<<<<<<< HEAD

params = {
            'save_path': "./video_repo/",
            'storage_mode': lt.storage_mode_t(2),
            'ti': lt.torrent_info(torrent)
        }
h = ses.add_torrent(params)

while True:
    s = h.status()
    msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
    print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
    time.sleep(1)
=======
def seeding(path, save_dir, enable=True):
    ses = lt.session()
    with open(path, 'rb') as f:
        torrent = lt.bdecode(f.read())
    params = {
                'save_path': save_dir,
                'storage_mode': lt.storage_mode_t(2),
                'ti': lt.torrent_info(torrent)
            }
    h = ses.add_torrent(params)
    while True:
    print(f"{datetime.datetime.utcnow()} - Start Sharing the original files")
    while enable:
        s = h.status()
        msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
        print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
        time.sleep(1)
    print(f"{datetime.datetime.utcnow()} - Stop Sharing the original files")


if __name__ == '__main__':
    seeding('./video_repo/video.torrent', './video_repo/')
>>>>>>> 17e3fbdbd5ad861773809d00125aa72201e2736c
