# Rukhsar Career + Finnish Assistant

A Streamlit dashboard for Rukhsar Zakria combining Finnish study, church/ecumenical opportunities, academic opportunities, funding, applications, career analytics, and Biblical Studies research radar.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload all files and folders from this repository, preserving the `data/` folder.
3. In Streamlit Community Cloud, choose the GitHub repository.
4. Set the main file path to `app.py`.
5. Deploy.

## Data note

Finnish progress and user-updated opportunity stages currently use browser cookies. Clearing browser/site data, changing browser, or changing device can remove that history. The JSON files in `data/` are repository seed/source files. A cloud database can be added later without changing the current storage keys.

## Important storage keys

Do not rename these during later updates unless a migration is deliberately implemented:

- `rukhsar_finnish_progress`
- `rukhsar_career_progress`
- `rukhsar_opportunity_pipeline`
