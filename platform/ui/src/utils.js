export function request(path, options) {
  // todo: remove hardcoded value
  const prefix = 'http://127.0.0.1:5000';

  return fetch(prefix + path, options);
}
