/**
 * WC86 - Wolf Club 86 - Event Emitter
 * Wrapper typé pour la communication ELI → STEPH
 */

import { createEventEmitter } from 'utils-event-emitter';
import type { EmitterEventMap, EmitterEventName, EmitterEventPayload } from './typesEmitterEvent';

// ============================================================================
// Event Emitter Instance
// ============================================================================

const emitter = createEventEmitter<EmitterEventMap>();

// ============================================================================
// Typed API for ELI (emit)
// ============================================================================

/**
 * Émet un event pour STEPH
 * Utilisé par les book event handlers
 */
export async function emit<T extends EmitterEventName>(
  event: T,
  ...args: EmitterEventPayload<T> extends Record<string, never>
    ? []
    : [payload: EmitterEventPayload<T>]
): Promise<void> {
  return emitter.emit(event, ...args);
}

// ============================================================================
// Typed API for STEPH (listen)
// ============================================================================

type EventCallback<T extends EmitterEventName> = EmitterEventPayload<T> extends Record<string, never>
  ? () => void | Promise<void>
  : (payload: EmitterEventPayload<T>) => void | Promise<void>;

/**
 * Écoute un event
 * Utilisé par STEPH pour les animations
 */
export function on<T extends EmitterEventName>(event: T, callback: EventCallback<T>): void {
  emitter.on(event, callback as never);
}

/**
 * Arrête d'écouter un event
 */
export function off<T extends EmitterEventName>(event: T, callback: EventCallback<T>): void {
  emitter.off(event, callback as never);
}

/**
 * Écoute un event une seule fois
 */
export function once<T extends EmitterEventName>(event: T, callback: EventCallback<T>): void {
  emitter.once(event, callback as never);
}

// ============================================================================
// Export pour GameContext
// ============================================================================

/**
 * Event emitter pour injection dans GameContext
 */
export const eventEmitter = {
  emit,
  on,
  off,
  once,
};
