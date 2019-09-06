## Two Sigma Connect: Rental Listing Inquiries

1. Enrole [in the competetion](https://www.kaggle.com/c/two-sigma-connect-rental-listing-inquiries/overview)
2. Get a key and save it in ``~/.kaggle/kaggle.json``
3. Run this command to get the data:
```
kaggle competitions download -c two-sigma-connect-rental-listing-inquiries
```
4. Unzip the receieved data:
```
unzip test.json.zip
unzip train.json.zip
unzip sample_submission.csv.zip
unzip images_sample.zip
```
5. Run ``code.py``
6. Prediction on test data is ready in ``submission_rf.csv`` file.