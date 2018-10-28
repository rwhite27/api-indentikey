import os
import face_recognition as fr

class Face:
    def generate_encodes(self, path):
        # Broken AF
        try:
            self.encodings = []
            for image in os.listdir(path):
                file = fr.load_image_file(f"{path}/{image}")
                self.encodings.append(fr.face_encodings(file))
            self.encodings = np.array(self.encodings)
            return self.encodings[0]
        except Exception as e:
            print(e)

    def load_encodes(self, file):
        self.encodes = np.load(file)[0]
    
    def save_encodes(encodes, file):
        try:
            self.encodes.dump(file)
        except Exception as e:
            print(e)
    
    def identify_face(self):
        pass
    
    def compare_faces(self):
        pass