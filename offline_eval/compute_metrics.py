import csv
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score

# تحميل الوصف المرجعي (ضع هنا قاموسك الكامل)
reference_dict = {
    "Animals 1.jpg": "three horses running through a grassy forest area",
    "Animals 2.jpg": "a colorful hummingbird hovering in mid-air",
    "Animals 3.jpg": "a gray and white cat sitting on a wooden pallet at sunset",
    "Animals 4.jpg": "a dog lying on grass with a tree and mountains behind",
    "Animals 5.jpg": "four horses grazing in a green field near trees",
    "Animals 6.jpg": "four penguins leaping out of the ocean water",
    "Animals 7.jpg": "an owl flying with wings spread against a clear sky",
    "Animals 8.jpg": "four zebras drinking from a calm waterhole",
    "Animals 9.jpg": "two penguins standing on a large rock under cloudy sky",
    "Animals 10.jpg": "a humpback whale breaching above the ocean surface",
    "Animals 11.jpg": "an arctic fox sitting on snowy ground",
    "Animals 12.jpg": "two elephants walking through a dry grassy savanna",
    "Animals 13.jpg": "a polar bear standing upright on snowy ground",
    "Animals 14.jpg": "a red squirrel facing forward against a dark background",
    "Animals 15.jpg": "a young raccoon sitting on a grassy field",
     "Building 1.jfif": "modern skyscrapers viewed from below with orange-lit elements",
    "Building 2.jpg": "a nighttime cityscape with skyscrapers and highway light trails",
    "Building 3.jpg": "a circular architectural structure viewed upward through an open center",
    "Building 4.jpg": "four tall skyscrapers forming a cross shape when viewed from below",
    "Building 5.jpg": "tall skyscrapers reflecting sunset light above an urban area",
    "Building 6.jpg": "tall skyscrapers reflecting sunset light above an urban area",
    "Building 7.jpg": "a gothic-style church on a hill with a statue of jesus at the top",
    "Building 8.jpg": "a tall cylindrical skyscraper under a pink and blue sky",
    "Building 9.jpg": "an aerial view of downtown chicago at sunset with lake michigan",
    "Building 10.jpg": "a city skyline at dusk with buildings reflected on the water",
    "Building 11.jpg": "a modern building with geometric shapes and a slanted glass facade",
    "Building 12.jpg": "the petronas twin towers illuminated at night above the city",
    "Building 13.jpg": "the empire state building lit at twilight with a crescent moon",
    "Building 14.jpg": "a tall skyscraper viewed from below with square window grid",
    "Building 15.jpg": "a minimalist white building with large windows and a cantilevered section",
         "Nature 1.jpg": "a rugged mountain landscape with rocky peaks and forested slopes",
    "Nature 2.jpg": "ocean waves crashing onto a sandy shore under a clear sky",
    "Nature 3.jpg": "a dense bamboo forest with tall vertical stalks and filtered sunlight",
    "Nature 4.jpg": "a metal pedestrian bridge leading into a lush green forest",
    "Nature 5.jpg": "lavender fields at sunset with warm golden light and distant mountains",
    "Nature 6.jpg": "a coastal sunset scene with colorful clouds and gentle waves",
    "Nature 7.jpg": "a dramatic coastal rock formation with a natural arch and crashing waves",
    "Nature 8.jpg": "a serene forest path surrounded by tall slender trees and warm sunlight",
    "Nature 9.jpg": "a grassy hill landscape with scattered trees and rolling green terrain",
    "Nature 10.jpg": "an ancient stone spiral labyrinth in a green valley at sunset",
    "Nature 11.jpg": "a tranquil mountain valley with a reflective river and dense pine forest",
    "Nature 12.jpg": "a sunlit granite monolith rising above a quiet meadow with tall pines",
    "Nature 13.jpg": "a lone figure standing on a rocky overlook facing layered mountains",
    "Nature 14.jpg": "a dramatic cliffside landscape with misty hills and a winding valley road",
    "Nature 15.jpg": "a golden wheat field with red poppies under a soft overcast sky",
         "Night 1.jpg": "a lively Japanese city street at night with neon signs and traffic",
    "Night 2.jpg": "a diagonal band of the Milky Way glowing across a dark sky",
    "Night 3.jpg": "a peaceful mountain silhouette beneath a clear star-filled night sky",
    "Night 4.jpg": "a dark forest road leading into the distance under a starry sky",
    "Night 5.jpg": "a bright full moon illuminating snowy mountain peaks at night",
    "Night 6.jpg": "a glowing ferris wheel reflecting colorful lights at night",
    "Night 7.jpg": "a deep blue starry sky with wispy clouds above dark trees",
    "Night 8.jpg": "a bright full moon rising behind pine trees and snowy mountains",
    "Night 9.jpg": "a quiet tree-lined road at night lit by a single warm streetlight",
    "Night 10.jpg": "a dim Japanese residential street at night with a passing train",
    "Night 11.jpg": "a starry twilight sky with pink and purple hues above rock formations",
    "Night 12.jpg": "a snowy mountain range under a deep blue night sky with a crescent moon",
    "Night 13.jpg": "a serene snow-covered mountain range beneath a star-filled night sky",
    "Night 14.jpg": "a vivid Milky Way with a bright meteor above mountain silhouettes",
    "Night 15.jpg": "a sweeping Milky Way stretching over snowy mountains with valley lights",
         "Person 1.jpg": "a peaceful lakeside scene with a person standing among tall grass",
    "Person 2.jpg": "a charming cobblestone street lined with historic buildings and trees",
    "Person 3.PNG": "a bright studio portrait of a smiling person with long wavy hair",
    "Person 4.jpg": "a cozy indoor scene of someone reading a book in warm lighting",
    "Person 5.jpg": "a close-up portrait of an older man with a white beard and glasses",
    "Person 6.jpg": "a street photographer holding a DSLR camera in a busy urban road",
    "Person 7.jpg": "a lone figure standing on a rocky ledge facing a sunlit mountain peak",
    "Person 8.jpg": "a person sitting on a concrete ledge framed by a large circular opening",
    "Person 9.jpg": "a person on a wooden swing facing a powerful waterfall",
    "Person 10.jpg": "a solitary figure sitting by the water looking toward a distant city skyline",
    "Person 11.jpg": "a man smiling warmly in a clean headshot portrait",
    "Person 12.jpg": "a young man smiling brightly in front of colorful neon lights",
    "Person 13.jpg": "a young man with curly hair wearing a black hoodie in an urban setting",
    "Person 14.jpg": "a smiling young man standing in a field of tall dry plants at golden hour",
    "Person 15.jpg": "a bearded young man on a rooftop with a blurred urban skyline",
    "Person 16.jpg": "a young woman smiling softly while leaning against a brick wall",
    "Person 17.jpg": "a bearded man with curly hair and glasses smiling warmly in a close-up portrait",
        "Things 1.jpg": "a small round wooden table with two black coffee cups in a vintage café",
    "Things 2.jpg": "a colorful salad bowl with crispy chicken and vegetables photographed from above",
    "Things 3.jpg": "a minimalist wooden headphone stand with black headphones on a desk",
    "Things 4.jpg": "an old weathered basketball hoop with chipped paint under a blue sky",
    "Things 5.jpg": "a close-up of a chessboard with black and white pieces in starting position",
    "Things 6.jpg": "a vintage shop entrance with framed art and a green bicycle outside",
    "Things 7.jpg": "a row of yellow hand straps hanging inside a public bus",
    "Things 8.jpg": "dark coats hanging on white plastic hangers on a clothing rack",
    "Things 9.jpg": "a close-up macro shot of a red plastic screw on lined paper",
    "Things 10.jpg": "five colorful pin buttons with slogans arranged on a wooden surface",
    "Things 11.jpg": "a vintage control room console with green-glowing CRT monitors",
    "Things 12.jpg": "a small glass bottle with a green cypress branch overlooking terraced fields",
    "Things 13.jpg": "a hand holding an old incandescent light bulb against a pastel sunset sky",
    "Things 14.jpg": "an open Russian book with eyeglasses resting on the pages",
    "Things 15.jpg": "a vintage cream rotary telephone next to a black cassette radio",
    "Things 16.jpg": "a solitary cast-iron park bench on a grassy slope",
    "Things 17.jpg": "a small glowing glass bottle on wet sand with ocean waves behind",
    "Things 18.jpg": "a flat-lay of antique hand tools on dark wooden planks",
    "Things 19.jpg": "a classic silver analog alarm clock on an open newspaper",
    "Things 20.jpg": "a small brown leather notebook with a pen and paper clip",
    "Things 21.jpg": "a collection of handmade and vintage objects arranged on the floor",
    "Things 22.jpg": "a retro brown tube television on a wooden side table",
    "Things 23.jpg": "a distressed white wooden chair with a pink balloon tied to it",
}

   

# مصفوفات لتخزين النتائج
bleu_base_scores = []
bleu_large_scores = []
meteor_base_scores = []
meteor_large_scores = []

smooth = SmoothingFunction().method1

# قراءة ملف النتائج
with open("results.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        image = row["image_name"]
        base_caption = row["base_caption"]
        large_caption = row["large_caption"]

        if image not in reference_dict:
            print(f"⚠️ لا يوجد وصف مرجعي للصورة: {image}")
            continue

        reference = reference_dict[image]

# حساب BLEU‑1
bleu_base = sentence_bleu(
    [reference.split()],
    base_caption.split(),
    weights=(1, 0, 0, 0),
    smoothing_function=smooth
)

bleu_large = sentence_bleu(
    [reference.split()],
    large_caption.split(),
    weights=(1, 0, 0, 0),
    smoothing_function=smooth
)

# حساب METEOR
meteor_b = meteor_score([reference.split()], base_caption.split())
meteor_l = meteor_score([reference.split()], large_caption.split())

bleu_base_scores.append(bleu_base)
bleu_large_scores.append(bleu_large)
meteor_base_scores.append(meteor_b)
meteor_large_scores.append(meteor_l)

# طباعة المتوسطات النهائية
print("\n===== FINAL AVERAGES =====")
print(f"BLEU‑1 Base Average  : {sum(bleu_base_scores)/len(bleu_base_scores):.4f}")
print(f"BLEU‑1 Large Average : {sum(bleu_large_scores)/len(bleu_large_scores):.4f}")
print(f"METEOR Base Average  : {sum(meteor_base_scores)/len(meteor_base_scores):.4f}")
print(f"METEOR Large Average : {sum(meteor_large_scores)/len(meteor_large_scores):.4f}")
