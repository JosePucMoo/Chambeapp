/** Convierte un valor a `YYYY-MM-DD` usando la fecha local. */
export const toDateString = (value: Date | string): string => {
  const date = value instanceof Date ? value : new Date(value);

  if (Number.isNaN(date.getTime())) return "";

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
};

/**
 * Interpreta una fecha `YYYY-MM-DD` (o ISO con hora) como fecha local.
 * Evita el desfase UTC al hacer `new Date("2026-10-15")`.
 */
export const parseDateOnly = (value: string): Date => {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);

  if (!match) {
    const fallback = new Date(value);
    return Number.isNaN(fallback.getTime()) ? new Date() : fallback;
  }

  return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
};

/** Clave estable por día: `YYYY-MM-DD`. */
export const dateKey = (value: Date | string): string =>
  value instanceof Date
    ? toDateString(value)
    : toDateString(parseDateOnly(value));

export const isSameDay = (a: Date, b: Date): boolean =>
  dateKey(a) === dateKey(b);

export const isToday = (value: Date): boolean => isSameDay(value, new Date());

export const addMonths = (value: Date, amount: number): Date =>
  new Date(value.getFullYear(), value.getMonth() + amount, 1);

export const isSameMonth = (a: Date, b: Date): boolean =>
  a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth();
