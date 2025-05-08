{{- define "common.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "nginx.selectorLabels" -}}
app.kubernetes.io/component: nginx
{{ include "common.labels" . }}
{{- end -}}

{{- define "app.selectorLabels" -}}
app.kubernetes.io/component: main-app
{{ include "common.labels" . }}
{{- end -}}

{{/* 
  Universal Resource Naming Helper
  Usage: {{ include "resource.name" (dict "ctx" . "component" "nginx" "suffix" "service") }}
*/}}
{{- define "resource.name" -}}
{{- $name := printf "%s-%s-%s" .ctx.Release.Name .component .suffix | lower | trunc 63 | trimSuffix "-" -}}
{{- $name -}}
{{- end -}}