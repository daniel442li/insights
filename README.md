# insights

An OCR program used to scan and analyze receipts. Created for VandyHack VII

**Inspiration:**
We realized that although there are numerous budgeting software options, none of them are truly accessible. They are too expensive, too complex, and too reliant on credit card purchase histories (a large inequity when you consider the high correlation between being low income and using cash more frequently). We realized that there was a need for insights, a platform that helps anyone and everyone budget.

**What it does:**
Users upload (or take) an image of a receipt. We then use OCR technology along with a string manipulation algorithm to gather vital information from the image’s input. Our data analysis algorithm analyzes the aforementioned information, generates a pie chart to visualize a breakdown of the user’s purchases, and provides the user with relevant suggestions for how to improve their spending habits. These are all displayed on our website.

**How we built it:**
We used pytesseract for our OCR. The output of pytesseract feeds into our two python algorithms, which do the bulk of our computation. We then connected this to our frontend by implementing our algorithms into endpoints of a Flask API. With Flask, we can utilize the powers of python with modern web design. Our front end, which was created primarily using HTML, CSS, JavaScript, and utilized Firebase, allows for seamless authentication and user image uploading.

**Challenges we ran into:**
We had a lot of issues integrating our different elements of code. We especially struggled with our matplotlib function to create a pie chart--due to a threading error. When we integrated it into our overall project, it caused the entire site to crash. Using packages that we didn’t fully understand led to a lot of complications. A ton of time was also spent connecting each member's code pieces together. Interweaving inputs to outputs especially across separate languages was quite a time consuming task.

**Accomplishments that we're proud of:**
The site works on its own and it is fairly efficient! We’re very proud of the speed of the algorithm as well as the UI design and code which was created with almost no prior experience. We are also extremely proud of the fact that we have a working demo that can actually help people.

**What we learned:**
We learned a lot about developing the front end for a platform and integrating code from different languages into one coherent product. We also learned how to use Firebase for modern user authentication as well as using modern data structures such as JSON on top of sending them across platforms using requests.

**What's next for insights:**
We will optimize the extremely rudimentary database currently being used to store user data and continue to better implement Firebase. We will work to improve user experience by showing more, and more relevant, information. We will address privacy concerns from having so much data on users.
