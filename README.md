# Music & Wellness

## Abstract
I set out on this project to build a machine learning model to predict the wellness of survey respondents. I learned along the way how to implement two python packages new to me that minimize PII and increased workflow efficiency. Model training proved to be quite challenging due to the less predictable nature of survey responses with self-assessments and time constraints.

## Package and workflow learnings
I got to implement new knowledge of two python packages and a workflow/pipeline technique during the script writing of this project.

- Python pkg: uuid - Assigned universally unique identifiers to replace timestamp data, something that I perceived to be potentially PII.
- Python pkg: imbalanced-learn - Used to resample a disproportionately small `y_test`
-  Python workflow: training.ipynb calls a function in preprocessing.py that runs the preprocessing script and returns only the variables relevant to the training and testing process.

## ML Performance
As stated in the abstract, performance of data modeling was quite a challenge. It's my finding that survey results dealing with subjective data such as music preferences and habits  are less predictable than datasets that may be more rooted in mathematical and scientific truth. In my training, I was able to achieve 60%-70% accuracy in predicting survey results who answered `music_effects = True`, but only 29% in predicting `music_effects = False` with recall and loss rates worse than a coin-flip.

## Future intention
- Exploration of further tuning existing models
- I am interested to take a step back and change the target data from `music_effects` to columns less subjective such as `listens_at_work` or `is_instrumentalist` to see if a more strong pattern exists.
- Integration with Spotify API

## Resources
- [MxMH Survey Results, Catherine Rasgaitis](https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results)
- [Python pkg: uuid](https://docs.python.org/3/library/uuid.html#uuid.uuid4)
- [Python pkg: imbalanced learn](https://pypi.org/project/imbalanced-learn/)
- [RFC 4211, IETF](https://datatracker.ietf.org/doc/html/rfc4122.html)
