import sys
import logging
from azure.cognitiveservices.vision.computervision import ComputerVisionClient


# Acquire the logger for this client library. Use 'azure' to affect both
# 'azure.core` and `azure.ai.vision.imageanalysis' libraries.
logger = logging.getLogger("azure")

# Set the desired logging level. logging.INFO or logging.DEBUG are good options.
logger.setLevel(logging.INFO)

# Direct logging output to stdout (the default):
handler = logging.StreamHandler(stream=sys.stdout)
# Or direct logging output to a file:
# handler = logging.FileHandler(filename = 'sample.log')
logger.addHandler(handler)

# Optional: change the default logging format. Here we add a timestamp.
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
handler.setFormatter(formatter)

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Define image URL
image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"

# Load image to analyze into a 'bytes' object
with open("sample.jpg", "rb") as f:
    image_data = f.read()

visual_features =[
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
        VisualFeatures.CAPTION,
        VisualFeatures.DENSE_CAPTIONS,
        VisualFeatures.READ,
        VisualFeatures.SMART_CROPS,
        VisualFeatures.PEOPLE,
    ]

# Analyze all visual features from an image stream. This will be a synchronously (blocking) call.
result = client.analyze_from_url(
    image_url=image_url,
    visual_features=visual_features,
    smart_crops_aspect_ratios=[0.9, 1.33],
    gender_neutral_caption=True,
    language="en"
)

# Print all analysis results to the console
print("Image analysis results:")

if result.caption is not None:
    print(" Caption:")
    print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

if result.dense_captions is not None:
    print(" Dense Captions:")
    for caption in result.dense_captions.list:
        print(f"   '{caption.text}', {caption.bounding_box}, Confidence: {caption.confidence:.4f}")

if result.read is not None:
    print(" Read:")
    for line in result.read.blocks[0].lines:
        print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
        for word in line.words:
            print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")

if result.tags is not None:
    print(" Tags:")
    for tag in result.tags.list:
        print(f"   '{tag.name}', Confidence {tag.confidence:.4f}")

if result.objects is not None:
    print(" Objects:")
    for object in result.objects.list:
        print(f"   '{object.tags[0].name}', {object.bounding_box}, Confidence: {object.tags[0].confidence:.4f}")

if result.people is not None:
    print(" People:")
    for person in result.people.list:
        print(f"   {person.bounding_box}, Confidence {person.confidence:.4f}")

if result.smart_crops is not None:
    print(" Smart Cropping:")
    for smart_crop in result.smart_crops.list:
        print(f"   Aspect ratio {smart_crop.aspect_ratio}: Smart crop {smart_crop.bounding_box}")

print(f" Image height: {result.metadata.height}")
print(f" Image width: {result.metadata.width}")
print(f" Model version: {result.model_version}")