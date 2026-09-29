import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Los vídeos demo son mudos: sin pista de audio vacía en el MP4.
Config.setMuted(true);
