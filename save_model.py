# save_model.py
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# 간단한 MobileNetV2 기반 모델 생성
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(1, activation='sigmoid')  # binary classification: plastic vs non-plastic
])

# 저장
model.save("plastic_classifier.h5")
print("✅ 모델 저장 완료: plastic_classifier.h5")
