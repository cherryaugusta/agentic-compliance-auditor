export type PaginatedResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type PolicyDocument = {
  id: number;
  title: string;
  document_type: string;
  source_name: string;
  jurisdiction: string | null;
  domain_area: string;
  owner_team: string | null;
  version_label: string;
  effective_date: string;
  supersedes_document: number | null;
  is_external_source: boolean;
  status: string;
  storage_path: string;
  sha256_checksum: string;
  content_text: string;
  section_count?: number;
  statement_count?: number;
};

export type DocumentSection = {
  id: number;
  document: number;
  section_index: number;
  heading: string | null;
  text: string;
  char_start: number;
  char_end: number;
  page_number: number | null;
  parser_confidence: number | null;
};

export type ControlStatement = {
  id: number;
  document: number;
  section: number;
  statement_type: string;
  raw_text: string;
  normalized_text: string;
  subject_entity: string | null;
  action_verb: string | null;
  condition_text: string | null;
  deadline_text: string | null;
  threshold_text: string | null;
  owner_role: string | null;
  schema_valid: boolean;
  extraction_confidence: number;
  extraction_version: string;
  embedding: number[] | null;
};

export type DocumentLineage = {
  id: number;
  parent_document: number;
  child_document: number;
  relationship_type: string;
};

export type VersionChain = {
  title: string;
  links: {
    parent_document: number;
    child_document: number;
    relationship_type: string;
  }[];
};

export type ComparisonRun = {
  id: number;
  source_document: number;
  run_type: string;
  target_document_ids: number[];
  config_snapshot: Record<string, unknown>;
  status: string;
  started_at: string | null;
  finished_at: string | null;
  correlation_id: string;
  created_at?: string;
  updated_at?: string;
};

export type ConflictFlag = {
  id: number;
  comparison_run: number;
  source_statement: number;
  target_statement: number | null;
  conflict_type: string;
  severity: string;
  status: string;
  confidence: number;
  requires_review: boolean;
  reason_summary: string;
  rules_triggered: string[];
  model_version: string | null;
  citation_count?: number;
  has_memo?: boolean;
};

export type EvidenceCitation = {
  id: number;
  conflict_flag: number;
  document: number;
  section: number;
  citation_role: string;
  excerpt_text: string;
};

export type FindingMemo = {
  id: number;
  conflict_flag: number;
  recommended_action: string;
  summary: string;
  structured_rationale: Record<string, unknown>;
  confidence: number;
  prompt_version: number | null;
};

export type ReviewTask = {
  id: number;
  conflict_flag: number;
  queue_name: string;
  assigned_to: number | null;
  status: string;
  reason_code: string;
  sla_due_at: string;
};

export type OverviewMetrics = {
  documents: number;
  comparison_runs: number;
  findings: number;
  review_tasks: number;
  eval_runs: number;
};

export type ReviewOpsMetrics = {
  unassigned: number;
  assigned: number;
  in_review: number;
  approved: number;
  dismissed: number;
  escalated: number;
};

export type ConflictMetrics = {
  open: number;
  needs_review: number;
  confirmed: number;
  dismissed: number;
  escalated: number;
  resolved: number;
  degraded_runs: number;
};

export type EvalReport = {
  contradiction_precision?: number;
  contradiction_recall?: number;
  stale_reference_accuracy?: number;
  citation_validity_rate?: number;
  review_routing_accuracy?: number;
};