import libtorrent as lt
import time


def seeding(path, save_dir):
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
        s = h.status()
        msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
        print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
        time.sleep(1)


if __name__ == '__main__':
    seeding('./video_repo/video.torrent', './video_repo/')
