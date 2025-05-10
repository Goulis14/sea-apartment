import os

from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from core.forms import ContactForm, NewsletterForm
from core.models import NewsletterSubscription
from sea_apartment import settings


def index(request):
    return render(request, 'index.html')


def rooms(request):
    static_dir = settings.STATICFILES_DIRS[0]

    def get_images(subfolder):
        folder = os.path.join(static_dir, f'images/kostis/{subfolder}')
        return sorted([
            f for f in os.listdir(folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ])

    context = {
        'garden_images': get_images('garden'),
        'thalassa_images': get_images('Thalassa'),
        'helios_images': get_images('Helios'),
    }
    return render(request, 'rooms.html', context)


def gallery(request):
    foto_dir = os.path.join(settings.BASE_DIR, 'core/static/images/kostis/FOTO')
    images = []

    for filename in os.listdir(foto_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            images.append(f'images/kostis/FOTO/{filename}')

    # Path to the "garden" directory
    garden_path = os.path.join(settings.BASE_DIR, 'core/static/images/kostis/garden')

    # List all files in the "garden" directory
    garden_images = []
    for file_name in os.listdir(garden_path):
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            garden_images.append(f'images/kostis/garden/{file_name}')

    context = {
        'images': images,
        'garden_images': garden_images
    }

    return render(request, 'gallery.html', context)


def amenities(request):
    return render(request, 'amenities.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Message from {name} <{email}>:\n\n{message}"

            try:
                # Send the message to the website's email
                email_message = EmailMessage(
                    subject=subject,
                    body=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[email],
                )
                email_message.send(fail_silently=False)

                # Send confirmation email to the user
                confirmation_subject = "Confirmation: We have received your message"
                confirmation_message = f"Hello {name},\n\nThank you for contacting us! We have received your message and will get back to you shortly.\n\nBest regards,\nThe Sea Apartments Team"
                confirmation_email = EmailMessage(
                    subject=confirmation_subject,
                    body=confirmation_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                confirmation_email.send(fail_silently=False)

                # Redirect to the thank-you page after successful submission
                return HttpResponseRedirect('/thank-you/')
            except Exception as e:
                # If sending email fails, display an error message to the user
                messages.error(request, "There was an issue sending your message. Please try again later.")
                return render(request, 'contact.html', {'form': form})

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save to database
            NewsletterSubscription.objects.get_or_create(email=email)

            # Send confirmation email
            subject = "Welcome to Sea Apartments Newsletter"
            message = (
                "Hello,\n\n"
                "Thank you for subscribing to our newsletter! "
                "You’ll now receive special offers, updates, and news about Sea Apartments.\n\n"
                "Warm regards,\n"
                "The Sea Apartments Team"
            )

            confirmation_email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            confirmation_email.send(fail_silently=False)

            return redirect('newsletter_thank_you')  # You’ll create this URL
    return redirect('/')  # fallback


def newsletter_thank_you(request):
    return render(request, 'newsletter_thank_you.html')
