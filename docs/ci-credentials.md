# Configuring Azure Face credentials for CI test runs

Follow these steps to let the GitHub Actions workflow run the live Azure Face API tests with your own credentials.

## 1. Collect the Azure Face API values
1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Open the **Face** resource you provisioned for this project (create one if you have not already).
3. In the left navigation, choose **Keys and Endpoint**.
4. Copy the **Endpoint** value and one of the **Key** values. You will paste both values into GitHub in the next step.

## 2. Store the credentials as GitHub Actions secrets
1. In your GitHub repository, navigate to **Settings → Secrets and variables → Actions**.
2. Select **New repository secret**.
3. Create a secret named `AZURE_FACE_ENDPOINT` and paste the endpoint URL that you copied from Azure.
4. Repeat the process to add another secret named `AZURE_FACE_API_KEY` using the key value from Azure.

> 💡 **Tip:** If you are configuring credentials for a fork, you must add the secrets in the forked repository's settings because secrets do not carry over from the upstream repository.

## 3. Trigger the CI workflow
1. Push a commit or open a pull request against a branch tracked by the workflow (the default is `main`/`master`). If you already pushed a change before adding secrets, you can instead open the **Actions** tab, choose the **CI** workflow, and run it manually with the **Run workflow** button.
2. GitHub Actions injects the secrets into the workflow as the `AZURE_FACE_ENDPOINT` and `AZURE_FACE_API_KEY` environment variables.
3. When `pytest` runs, the integration tests detect that the environment variables are populated and execute the live Azure Face API checks.

## 4. (Optional) Verify locally
To mimic the CI environment locally, export the same variables before running the tests:

```bash
export AZURE_FACE_ENDPOINT="https://<your-face-resource>.cognitiveservices.azure.com/"
export AZURE_FACE_API_KEY="<your-face-api-key>"
pytest
```

If the credentials are valid, the integration tests will run instead of being skipped.
