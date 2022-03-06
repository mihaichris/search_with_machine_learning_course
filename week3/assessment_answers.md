## For classifying product names to categories:
### What precision (P@1) were you able to achieve?
0.949, with text preprocessing, min product count=100, category depth=3

### What fastText parameters did you use?
 I used parameters: `epoch` 25 and `ngram` 2

### How did you transform the product names?
Stripped the punctuation, lowercased the keywords and used Snowball Stemming for strem keywords from phrase.

### How did you prune infrequent category labels, and how did that affect your precision?
Implemented `min_product` parameter to enforce a minimum number of products per category for the thresholds 50, 100, 200

Results over different thresholds, with transformed product names:

| min_product | n_words | n_labels | P@1   | R@1   |
|-------------|---------|----------|-------|-------|
| 50          | 21938   | 93       | 0.983 | 0.983 |
| 100         | 21778   | 80       | 0.949 | 0.949 |
| 200         | 21505   | 67       | 0.983 | 0.955 |]


Increasing `min_product` increased our overall precision, but reduced the coverage of more infrequent category labels. Ther classifier achieves higher precision by discarding labels for which it would have lower confidence, so there is a conscious tradeoff to be made here

### How did you prune the category tree, and how did that affect your precision?

Results over different category depths, with transformed product names, and min_product=50:

| cat_depth | n_words | n_labels | P@1   | R@1   |
|-----------|---------|----------|-------|-------|
| 1         | 19053   | 512      | 0.667 | 0.725 |
| 2         | 20866   | 270      | 0.801 | 0.799 |
| 3         | 21938   | 93       | 0.983 | 0.955 |

## For deriving synonyms from content:
### What 20 tokens did you use for evaluation?
Product types
- phone
- laptop
- battery
- camera
- keyboard

Brands
- sony
- apple
- samsung
- lenovo
- dell

Models
- iphone
- thinkpad
- playstation
- ipad
- s3

Attributes
- black
- silver
- windows
- mac
- green

### What fastText parameters did you use?
- `minCount` for 10, 20, 50

### How did you transform the product names?
I stripped the punctuation, lowercasing the words and used snowball stemmng. Same as level 1.

### What threshold score did you use?
0.93

### What synonyms did you obtain for those tokens?
| **query**       | **synonyms (including scores)**                                                                                                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| phone      | mobil 0.900374, unlock 0.880669, earphon 0.871344, motorola 0.869082, 4g 0.869076, cell 0.863492, verizon 0.862635, speakerphon 0.861238, htc 0.858955, iphon 0.845068 |
| laptop     | inspiron 0.978132, i3 0.976608, lenovo 0.976278, processor 0.97484, xps 0.971059, vaio 0.970249, aspir 0.969161, athlon 0.968943, i7 0.967736, x2 0.9663 
| battery     | batteri 0.986491, recharg 0.939317, carri 0.938187, lenmar 0.937145, digipow 0.927454, tripod 0.9246, telephon 0.918068, casio 0.914831, trip 0.914693, accessori 0.914132
| camera     | shot 0.992704, eo 0.991206, nikon 0.991097, 0mp 0.990231, megapixel 0.9899, 3mp 0.988435, rebel 0.98837, xs 0.987542, d90 0.987463, 1mp 0.987012
| keyboard     | keyboard 0.991552, tribeca 0.961231, board 0.956594, scoreboard 0.950685, dashboard 0.946998, folio 0.94577, skin 0.941065, musicskin 0.938052, pad 0.937948, shield 0.937931
| sony       | onyx 0.979699, deep 0.962531, factori 0.957017, ibm 0.951854, matt 0.946209, datel 0.945513, ceram 0.945272, ideapad 0.944013, delonghi 0.943984, messeng 0.940068 
| apple           | speck 0.957051, sound 0.95444, miami 0.950016, russound 0.940206, outfit 0.940029, numark 0.939576, cincinnati 0.936033, arizona 0.934033, skullcandi 0.932286, stereo 0.930977  |
| samsung         | samsung 0.986607, lg 0.886898, sharp 0.882205, 32 0.855607, 120hz 0.833572, 720p 0.83153, 60hz 0.830947, aquo 0.828086, panason 0.823668, 1080p 0.823446                         
| lenovo         | i3 0.98008, 6gb 0.97756, laptop 0.976278, vaio 0.976174, pentium 0.972884, processor 0.972302, xps 0.971798, essentio 0.971019, i7 0.96993, 3gb 0.968108    
| dell            | xentri 0.943158, cell 0.918245, htc 0.905712, evo 0.901603, no 0.897648, invisibleshield 0.896585, commut 0.895587, dell 0.891676, droid 0.886225, 4g 0.884393                 
| iphone          | phone 0.946795, motorola 0.943585, iphon 0.941047, verizon 0.933045, bluetooth 0.924805, unlock 0.916583, blackberri 0.908568, 4g 0.904746, nokia 0.902537, shell 0.901644       |
| thinkpad        | ibm 0.973248, lenovo 0.965258, ideapad 0.954518, factori 0.95432, laptop 0.949409, vaio 0.942251, inspiron 0.941811, dell 0.938687, e 0.935412, eee 0.935337                     |
| playstation        | dawn 0.967199, ps 0.966702, limit 0.961784, edit 0.958794, world 0.957837, danc 0, 957825, duti 0.953722, wild 0.953131, gba 0.952184, warrior 0.951752              |
| ipad            | folio 0.989514, 3rd 0.963269, 4th 0.958918, tribeca 0.958223, 4s 0.954354, 3g 0.953308, generat 0.952774, nano 0.950117, otterbox 0.950056, charger 0.948895                     |
| s3        | ninja 0.986311, dsi 0.981064, madden 0.980423, spyro 0.973903, psp 0.972277, rise 0.971059, 2010 0.970122, fantasi 0.968156, nfl 0.96591, battl 0.965698  
| black           | cleaner 0.877261, slider 0.874202, open 0.843965, white 0.843472, cellar 0.84054, orang 0.839546, gel 0.837472, glove 0.835101, cellular 0.829889, pure 0.824599                 |
| silver          | cyber 0.950368, handycam 0.946944, dcr 0.910118, camcord 0.906342, dsc 0.902267, lumix 0.901322, tripod 0.898695, blue 0.894917, red 0.893617, mini 0.891664                     |
| windows         | window 0.999168, edit 0.959025, of 0.955926, adventur 0.948302, wii 0.945745, world 0.94547, advanc 0.945223, gamecub 0.942082, 360 0.941311, nintendo 0.937693                  |
| steel           | bisqu 0.974568, stainless 0.973962, oven 0.972026, hood 0.97095, gas 0.967612, biscuit 0.966582, microwav 0.966115, maytag 0.965482, architect 0.960114, galleri 0.958254        |
| green | tiffen 0.943733, jabra 0.942374, fishfind 0.940274, mix 0.937022, glove 0.936701, casio 0.933453, dora 0.931864, s1 0.931333, care 0.930913, maxel 0.92941