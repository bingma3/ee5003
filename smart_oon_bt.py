import libtorrent as lt
import time
import datetime


class SmartOohBT:
    def __init__(self):
        pass

    @staticmethod
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
        print(f"{datetime.datetime.utcnow()} - Start Sharing the original files")
        while enable:
            s = h.status()
            msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
            print((msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)), end=' ')
            time.sleep(1)
        print(f"{datetime.datetime.utcnow()} - Stop Sharing the original files")

    @staticmethod
    def make_seed(path, save_dir, torrent_path):    # create a torrent file
        """
        :param path: the path of the target data
        :param save_dir: directory for restore the hash pieces
        :param torrent_path: the path of the torrent file
        """
        fs = lt.file_storage()
        lt.add_files(fs, path)
        t = lt.create_torrent(fs)
        t.add_tracker("http://192.168.1.85/announce", 0)
        t.add_tracker("udp://open.stealth.si:80/announce", 0)
        t.add_node("router.utorrent.com", 6881)
        t.add_node("dht.transmissionbt.com", 6881)
        t.set_creator("smartooh torrent")
        t.set_comment("smartooh video")
        t.set_priv(True)
        lt.set_piece_hashes(t, save_dir)
        with open(torrent_path, "wb") as f:
            f.write(lt.bencode(t.generate()))


if __name__ == '__main__':
    SmartOohBT.seeding('./video_repo/video.torrent', './video_repo/')
