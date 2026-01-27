import { writable, get } from 'svelte/store';
import { aiGenerate, getAIThread, getAISettings } from '$lib/api';
import { browser } from '$app/environment';

function createAiChatStore() {
	const initialState = {
		threadId: null,
		messages: [],
		loading: false,
		error: null,
		messageCount: 0,
		canCreateProject: false,
		requiresLogin: false,
		settings: {
			maxAnonymousMessages: 5,
			minMessagesForProject: 3,
			maxAnonymousDrafts: 2
		}
	};

	const { subscribe, set, update } = writable(initialState);

	// Generate unique session ID for anonymous users
	function getSessionId() {
		if (!browser) return null;

		let sessionId = localStorage.getItem('ai_session_id');
		if (!sessionId) {
			sessionId = 'session-' + crypto.randomUUID();
			localStorage.setItem('ai_session_id', sessionId);
		}
		return sessionId;
	}

	// Load settings from API
	async function loadSettings() {
		try {
			const settings = await getAISettings();
			update((state) => ({
				...state,
				settings: {
					maxAnonymousMessages: settings.max_anonymous_messages,
					minMessagesForProject: settings.min_messages_for_project,
					maxAnonymousDrafts: settings.max_anonymous_drafts
				}
			}));
		} catch (e) {
			console.error('Failed to load AI settings:', e);
		}
	}

	// Load existing thread
	async function loadThread(threadId) {
		// Reset state before loading new thread
		update((state) => ({
			...state,
			threadId: null,
			messages: [],
			messageCount: 0,
			canCreateProject: false,
			requiresLogin: false,
			loading: true,
			error: null
		}));

		try {
			const thread = await getAIThread(threadId);

			// Convert messages to our format
			const messages = thread.messages.map((msg) => ({
				id: msg.id,
				content: msg.content,
				isAssistant: msg.is_assistant,
				createdAt: new Date(msg.created_at)
			}));

			// Calculate canCreateProject based on loaded thread
			const currentState = get({ subscribe });
			const canCreate = thread.user_message_count >= currentState.settings.minMessagesForProject;

			update((state) => ({
				...state,
				threadId: thread.id,
				messages,
				messageCount: thread.user_message_count,
				canCreateProject: canCreate,
				loading: false
			}));

			return thread;
		} catch (e) {
			update((state) => ({
				...state,
				loading: false,
				error: e.message
			}));
			throw e;
		}
	}

	// Send a message
	async function sendMessage(content) {
		const state = get({ subscribe });

		// Add user message immediately (optimistic update)
		const userMessage = {
			id: 'temp-' + Date.now(),
			content,
			isAssistant: false,
			createdAt: new Date()
		};

		update((s) => ({
			...s,
			messages: [...s.messages, userMessage],
			loading: true,
			error: null
		}));

		try {
			const response = await aiGenerate(content, state.threadId, getSessionId());

			// Add assistant message
			const assistantMessage = {
				id: 'ai-' + Date.now(),
				content: response.raw_reply,
				htmlContent: response.reply,
				isAssistant: true,
				createdAt: new Date()
			};

			update((s) => ({
				...s,
				threadId: response.thread_id,
				messages: [...s.messages, assistantMessage],
				messageCount: response.message_count,
				canCreateProject: response.can_create_project,
				requiresLogin: response.requires_login,
				loading: false
			}));

			// Store thread ID in localStorage for persistence
			if (browser && response.thread_id) {
				localStorage.setItem('ai_thread_id', response.thread_id);
			}

			return response;
		} catch (e) {
			update((s) => ({
				...s,
				loading: false,
				error: e.message
			}));
			throw e;
		}
	}

	// Reset the chat
	function reset() {
		if (browser) {
			localStorage.removeItem('ai_thread_id');
		}
		// Reset state but preserve loaded settings
		update((state) => ({
			...initialState,
			settings: state.settings
		}));
	}

	// Initialize from localStorage
	function init() {
		if (browser) {
			const savedThreadId = localStorage.getItem('ai_thread_id');
			if (savedThreadId) {
				loadThread(savedThreadId).catch(() => {
					// Thread not found, reset
					localStorage.removeItem('ai_thread_id');
				});
			}
		}
		loadSettings();
	}

	return {
		subscribe,
		sendMessage,
		loadThread,
		loadSettings,
		reset,
		init,
		getSessionId
	};
}

export const aiChat = createAiChatStore();
