<?php
/*
 * Legacy hostname retirement.
 *
 * The site is served from a single docroot that answers on several hostnames:
 *   - data.opengamedata.io  : canonical host for the data site (keep serving)
 *   - opengamedata.fielddaylab.wisc.edu / .org : legacy hostnames (retired)
 *
 * Requests for a retired hostname are permanently redirected to the project's
 * public site. This only affects the PHP pages; raw dataset paths under /data/
 * are plain files served by Apache and are deliberately left alone, because the
 * files API still hands out download URLs on the legacy hostname.
 */

const LEGACY_HOSTS = [
    'opengamedata.fielddaylab.wisc.edu',
    'opengamedata.fielddaylab.org',
];

const CANONICAL_SITE = 'https://opengamedata.io/';

function redirect_legacy_hosts(): void
{
    if (empty($_SERVER['HTTP_HOST'])) {
        return;
    }

    // Strip any port and normalize case before comparing.
    $host = strtolower(explode(':', $_SERVER['HTTP_HOST'])[0]);

    if (!in_array($host, LEGACY_HOSTS, true)) {
        return;
    }

    if (!headers_sent()) {
        header('Location: ' . CANONICAL_SITE, true, 301);
        header('Cache-Control: max-age=3600');
    }
    exit;
}

redirect_legacy_hosts();
