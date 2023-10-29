import cv2

class Video():
    def __init__(self):
        self.cam=cv2.VideoCapture(0)
        self.width=int(self.cam.get(3))
        self.height=int(self.cam.get(4))
        self.fps=30
        self.format=cv2.VideoWriter_fourcc(*'mp4v')
        self.output=cv2.VideoWriter('crash.mp4',self.format,self.fps,(self.width,self.height))

    def recording(self):      
        while True:
            ret, frame = self.cam.read()
            if not ret:
                break

            self.output.write(frame)

            cv2.imshow('Recording', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 종료 시 정리
        self.cam.release()
        self.output.release()
        cv2.destroyAllWindows()