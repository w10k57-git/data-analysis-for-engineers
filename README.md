# Analiza danych inżynierskich z wykorzystaniem języka Python

Python course materials for engineering master's students. This course assumes no to very little Python familiarity at the beginning. The course starts with fundamental concepts in Python, and then moving through basic scripting and numerical calculations using `math` and `numpy`. In the latter part of the course, students learn how to load data from various sources, including web scraping. On the fifth laboratory, students learn how to perform an Exploratory Data Analysis, followed by some statistical analysis of the results. They also study the interactions with databases. The course culminates in learning about basic interaction with chatbots, including prompting strategies.

## Preparation of the repository for laboratory class

Before starting, make sure you have the following installed:

- **uv**
- **Visual Studio Code**
- **Git**

## Setup

### 1. Clone the Repository

Clone this repository into a folder named with your **student index number**.

Replace `123456` with your actual index number:

```bash
git clone https://github.com/w10k57-git/data-analysis.git 123456
cd 123456
```

**Example:** If your index number is `987654`, you would run:

```bash
git clone https://github.com/w10k57-git/data-analysis.git 987654
cd 987654
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Git

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

Verify your configuration:

```bash
git config user.name
git config user.email
```

### 4. Create Your Working Branch

```bash
git checkout -b lab
```

**Important:** All students work on the `lab` branch. Never commit to `main`!

## Daily Workflow

### Getting Instructor Updates

When the instructor publishes new materials:

```bash
git checkout main
git pull origin main
git checkout lab
git merge main
```

### Working on Tasks

All your work should be done in the `tasks/` directory:

```bash
cd tasks/
uv run python your_script.py
```

### Committing Your Work

```bash
git add .
git commit -m "Complete task XYZ"
```

**Note:** Your work stays local. You don't push to the remote repository.

## Examples

## Repository Structure

```
123456/  (your index number)
├── examples/       # Code examples and exercises
├── tasks/          # YOUR workspace - work here!
├── src/            # Utility functions you can use
└── data/           # Data files for the course
```

## Git Workflow Summary

- **`main`** - Course materials from instructor (read-only)
- **`lab`** - Your working branch (all students use this name)

### Key Commands

```bash
# Check status
git status

# View history
git log --oneline

# See changes
git diff
```

## Complete Setup Checklist

- [ ] Clone repository into folder named with your index number
- [ ] Run `uv sync` to install dependencies
- [ ] Configure `git config user.name` and `git config user.email`
- [ ] Create `lab` branch with `git checkout -b lab`

---

Happy coding! 🚀
