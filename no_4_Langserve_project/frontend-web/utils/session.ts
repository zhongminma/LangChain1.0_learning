export function getSessionId(): string{
    let sid = localStorage.getItem("chat_session_id")
    if (!sid) {
        sid = crypto.randomUUID();
        localStorage.setItem("chat_session_id", sid)
    }
    return sid;
}