export type DateFormatStyle = "short" | "medium" | "long" | "relative";

export const formatDate = (
  dateString: string | null | undefined,
  style: DateFormatStyle = "medium",
  locale: string = "es-MX",
): string => {
  if (!dateString) return "--";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return "Fecha inválida";

  switch (style) {
    case "short":
      // Output: 30/09/2026
      return new Intl.DateTimeFormat(locale, {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      }).format(date);

    case "medium":
      // Output: 30 sep 2026
      return new Intl.DateTimeFormat(locale, {
        day: "2-digit",
        month: "short",
        year: "numeric",
      }).format(date);

    case "long":
      // Output: 30 de septiembre de 2026
      return new Intl.DateTimeFormat(locale, {
        day: "2-digit",
        month: "long",
        year: "numeric",
      }).format(date);

    case "relative":
      // Output: "en 2 días" or "hace 3 días"
      return getRelativeTime(date, locale);

    default:
      return date.toLocaleDateString(locale);
  }
};

const getRelativeTime = (date: Date, locale: string): string => {
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  const daysDifference = Math.round(
    (date.getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24),
  );

  return rtf.format(daysDifference, "day");
};
