// L: settings for all files: the agents, their access, the skills, the file's chats.
import {useState} from "react";
import {api} from "../api";
import {openLibrary} from "../actions";
import {familyOf, plural, shortPath} from "../lib/format";
import {get, set, useApp} from "../store";
import {Icon, Mark} from "./bits";
import {AccessRadios, Lbl} from "./Menus";

const INSTALL: Record<string, string> = {claude: "https://docs.anthropic.com/en/docs/claude-code", codex: "https://github.com/openai/codex",
  pi: "https://github.com/badlogic/pi-mono"};
const chats = (n: number) => plural(n, ["чат", "чата", "чатов"]);

export const BackTop = ({id = "back", title, sub, onBack, children}: {id?: string; title: string; sub: string; onBack: () => void; children?: React.ReactNode}) => (
  <header className="backtop"><button className="iconbtn" id={id} title="Назад" aria-label="Назад" onClick={onBack}><Icon n="back" /></button>
    <b>{title}</b><small>{sub}</small>{children}</header>
);

export function Settings({hidden}: {hidden?: boolean}) {
  const {S} = useApp(), here = S.chats.length, [asking, setAsking] = useState(false);
  const clear = async () => {  // W: asked in its own row, with the count
    setAsking(false);
    for (const c of [...get().S.chats]) await api("/api/delete", {chat: c.id});
    set({chat: null});
  };
  return (
    <div className="settings page" id="settings" hidden={hidden}>
      <BackTop title="Настройки" sub="для всех файлов" onBack={() => set({settingsOpen: false})} />
      <div className="body" style={{gap: 8, padding: "8px 12px 16px"}}>
        <Lbl>Агенты</Lbl>
        <div className="card">
          {S.agents.map((a) => (
            <div className="crow" key={a.id}><span className="lead"><Mark id={a.id} /></span>
              <span className="txt"><span style={a.ok ? undefined : {color: "var(--dim)"}}>{a.name}</span>
                <small title={a.account || a.path || ""}>{a.account ? `аккаунт ${shortPath(a.account)}` : a.ok ? [((a.version || "").match(/[\d.]+/) || [""])[0], shortPath(a.path)].filter(Boolean).join(" · ") : "не найден в PATH"}</small></span>
              {a.ok ? <span className="count">{plural(a.models.length, ["модель", "модели", "моделей"])}</span>
                : <a className="btn" href={INSTALL[familyOf(a.id)]} target="_blank">Как установить</a>}
            </div>
          ))}
        </div>
        <Lbl>Доступ агента</Lbl>
        <div className="card"><AccessRadios mode={S.settings.mode} /></div>
        <Lbl>Навыки</Lbl>
        <div className="card">
          <button className="crow" id="libraryBtn" onClick={openLibrary}><span className="lead"><Icon n="puzzle" /></span>
            <span className="txt"><span>Все навыки</span><small>библиотека · {(S.skills || []).length} · группы и режимы</small></span><span className="lead">›</span></button>
        </div>
        <Lbl>Чаты</Lbl>
        {asking ? (
          <div className="card confirm" id="clearConfirm">
            <b>Удалить {chats(here)} файла {S.doc.name}?</b>
            <small>Вместе с историей сообщений. Правки на холсте останутся.</small>
            <div className="row"><span className="grow" /><button className="btn" onClick={() => setAsking(false)}>Отмена</button>
              <button className="btn danger solid" id="clearYes" onClick={clear}>Удалить {chats(here)}</button></div>
          </div>
        ) : (
          <div className="card">
            <div className="crow"><span className="txt"><span>{S.doc.name ? `У этого файла ${chats(here)}` : "Файл не открыт"}</span><small>~/.local/state/figcraft-agent</small></span>
              <button className="btn danger" id="clear" disabled={!here} onClick={() => setAsking(true)}>Очистить</button></div>
          </div>
        )}
        <div className="caption" style={{padding: "0 4px"}}>Агенты работают через свои CLI и ваши подписки — ключи не нужны. Чат продолжает сессию агента.</div>
      </div>
    </div>
  );
}
