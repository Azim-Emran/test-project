# ai_learning_assistant
AN AI-Powered Personalized Learning Assistant

The most secure and recommended way for sensitive information like API keys in GitHub Codespaces is to use Codespaces secrets.

Here's a step-by-step guide:

1. Go to your GitHub Repository Settings:

Navigate to your repository on GitHub.com (the one your Codespace is based on).
Click on the "Settings" tab.

2. Access Codespaces Secrets:

In the left sidebar, under "Security" or "Security and analysis," click on "Secrets and variables."
Then, click on "Codespaces."

3. Add a New Codespaces Secret:

Click the "New repository secret" button (or "New secret" if it's an organization-level secret).
Name: Enter OPENAI_API_KEY (this must match the name your code uses with os.getenv()).
Value: Paste your actual OpenAI API key here.
Click "Add secret."

4. Restart Your Codespace:

For the new secret to be recognized, you'll need to stop and restart your existing Codespace.

In your Codespace, open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P).
Search for "Codespaces: Stop Current Codespace" and select it.
Once stopped, you can restart it from the GitHub Codespaces page or by re-opening the Codespace from your repository.
Alternatively, if you create a new Codespace, the secret will be available automatically.

Libraries installed
- pip install flask flask_login flask_sqlalchemy
- pip install python-dotenv
- pip install openai
- pip install pandas numpy scikit-learn
- pip install joblib


# Recommended Workflow for Collaboration:
_______________________________________________________________
A good practice in a collaborative environment is often:
_______________________________________________________________
Start your day (or before starting work on a new task):

terminal code:
1. git pull origin main  # Get the latest changes from the main branch
_______________________________________________________________
Make your changes.
Stage your changes:

terminal code:
2. git add .
_______________________________________________________________
Commit your changes:

3. git commit -m "Meaningful commit message"
_______________________________________________________________
Before pushing, pull again (to be safe):

terminal code:
4. git pull origin main

(This ensures you have the absolute latest version and resolve any conflicts before pushing your changes.)
_______________________________________________________________
Push your changes:

terminal code:
5. git push origin main
_______________________________________________________________
By consistently pulling before you start work and before you push, you minimize the chances of large, complex merge conflicts and keep your local repository synchronized with the team's progress.
______________________________________________________________
6. Handle potential merge conflicts:
If other collaborators have made changes to the same lines of code that you've also modified, Git cannot automatically merge them. This will result in a merge conflict.

Git will notify you of the conflicted files.
You'll need to open these files in your code editor. Git will insert special markers to show you the conflicting sections:
<<<<<<< HEAD
Your local changes here
=======
Changes from the remote repository here
>>>>>>> origin/main
Resolve the conflict: Manually edit the file to keep the desired code (could be yours, theirs, or a combination). Remove the <<<<<<<, =======, and >>>>>>> markers.
Stage the resolved file:
Bash

git add conflicted_file_name.js
Commit the merge: Git will often provide a default merge commit message. You can accept it or modify it.
Bash

git commit -m "Merge remote-tracking branch 'origin/main'"

7. git stash

If you used git stash earlier, remember to "git stash pop" after pulling and committing to reapply your stashed changes, and then resolve any new conflicts that might arise.

Apply Your Stashed Changes (git stash pop)
This is the most common next step. git stash pop will reapply the changes you stashed earlier and then remove them from your stash list.
________________________________________________________________

# Flask Migration

1. app.py to include: 
    from flask_migrate import Migrate 
    db.init_app(app)
    migrate = Migrate(app, db) 

2. Type in the terminal
    set FLASK_APP=app.py    # Windows cmd

3. Run flask --help again.
    (You should now see db listed under "Commands".)

4. Initialize the migration repository (if you haven't, or if you need to re-initialize).
    flask db init (run only once)

5. Update flask db
    flask db update

6. Run migration command
    flask db migrate -m "Update user models"

This should now successfully create a new migration script in your migrations/versions directory, reflecting the changes to your models (or the initial state if this is the first proper migration).