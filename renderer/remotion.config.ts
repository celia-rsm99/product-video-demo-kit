import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Los vídeos demo son mudos: sin pista de audio vacía en el MP4. Los vídeos con
// voz se renderizan con `tools/render_video.py --con-audio` (pasa --muted=false).
Config.setMuted(true);
