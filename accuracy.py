import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load trained model
model = load_model(r"D:\Brain_tumor_detection\my_brain_tumor_mobilenetv2.h5")

# Prepare test data
test_datagen = ImageDataGenerator(rescale=1./255)
test_data = test_datagen.flow_from_directory(
    r"D:\Brain_tumor_detection\Brain\Testing",
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Evaluate the model
loss, acc = model.evaluate(test_data)
print(f"✅ Test Accuracy: {acc*100:.2f}%")