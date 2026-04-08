export const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const phoneRegex = /^\+1\d{10}$/;

export function validateOutreachForm(form) {
  const name = form.name.trim();
  const email = form.email.trim();
  const phone = form.phone.trim();
  const message = form.message.trim();

  if (!name) return "Name is required.";
  if (name.length < 2) return "Enter a valid name.";
  if (!message) return "Message is required.";

  if (!email && !phone) {
    return "Enter at least an email or phone number.";
  }

  if (email && !emailRegex.test(email)) {
    return "Enter a valid email.";
  }

  if (phone && !phoneRegex.test(phone)) {
    return "Phone must match +1XXXXXXXXXX.";
  }

  return "";
}