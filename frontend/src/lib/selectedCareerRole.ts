/**
 * Selected role + optional location store.
 *
 * Keeps the most recently selected career role in memory so the application
 * form can pre-select it when the careers page is extended. The value is
 * also persisted to localStorage so a refresh does not lose the selection.
 */

import type { CareerRole } from "./careerData";

const STORAGE_KEY = "vr-coatings-selected-career-role";

type Listener = (role: CareerRole | null) => void;
const listeners = new Set<Listener>();
let current: CareerRole | null = null;

function emit() {
  listeners.forEach((fn) => fn(current));
}

export function getSelectedCareerRole(): CareerRole | null {
  if (current) return current;
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    current = JSON.parse(raw) as CareerRole;
  } catch {
    current = null;
  }
  return current;
}

export function setSelectedCareerRole(role: CareerRole | null) {
  current = role;
  if (typeof window !== "undefined") {
    try {
      if (role === null) {
        window.localStorage.removeItem(STORAGE_KEY);
      } else {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(role));
      }
    } catch {
      /* ignore storage failures */
    }
  }
  emit();
}

export function subscribeSelectedCareerRole(listener: Listener): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}