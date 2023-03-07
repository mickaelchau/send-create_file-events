from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECT_ID = "micka-cloud-run-365208"
TOPIC_NAME = "create-file"
DIRECTORY = "/mnt/filestore_dir"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("File created:", event.src_path)
            message = event.src_path.encode("utf-8")
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
            try:
                publisher.publish(topic_path, message)
            except NotFound:
                print("Topic not found:", topic_path)
            else:
                future = publisher.publish(topic_path, data=message)
                print("Notification sent:", future.result())

observer = Observer()
observer.schedule(MyHandler(), path=DIRECTORY)
observer.start()

try:
    print("Lsitening for created files in the path: /mnt/filestore_dir")
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()

