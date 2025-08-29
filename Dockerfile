# Use a slim Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for Python for production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and switch to a non-root user for security
RUN useradd -m -u 1000 user
USER user

# Set the working directory
WORKDIR /home/user/app
ENV PATH="/home/user/.local/bin:${PATH}"

# Copy and install dependencies
COPY --chown=user gui/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY --chown=user gui/ .

# Run collectstatic to gather all static files
RUN SECRET_KEY="dummy" STATIC_ROOT="/home/user/app/staticfiles" python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gui.wsgi"]