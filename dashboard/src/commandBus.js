const handlers = {};
export function on(type, fn) { (handlers[type] ||= []).push(fn); }
export function dispatch(cmd) { (handlers[cmd.type] || []).forEach(fn => fn(cmd)); }