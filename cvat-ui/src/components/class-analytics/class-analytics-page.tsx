// Copyright (C) CVAT.ai Corporation
//
// SPDX-License-Identifier: MIT

import './styles.scss';

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useParams } from 'react-router';
import { Row, Col } from 'antd/lib/grid';
import Alert from 'antd/lib/alert';
import Empty from 'antd/lib/empty';
import InputNumber from 'antd/lib/input-number';
import Result from 'antd/lib/result';
import Spin from 'antd/lib/spin';
import Typography from 'antd/lib/typography';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

import GoBackButton from 'components/common/go-back-button';
import { getCore } from 'cvat-core-wrapper';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface LabelCount {
    label: string;
    count: number;
}

interface CountsResponse {
    task_id: number;
    job_id: number | null;
    counts: LabelCount[];
}

type LoadState = 'loading' | 'ready' | 'empty' | 'error';

const core = getCore();

function wsUrl(taskId: number): string {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.host}/api/test/ws/tasks/${taskId}/annotation-counts`;
}

function ClassAnalyticsPage(): JSX.Element {
    const { tid } = useParams<{ tid: string }>();
    const taskId = Number(tid);
    const [jobFilter, setJobFilter] = useState<number | null>(null);
    const [payload, setPayload] = useState<CountsResponse | null>(null);
    const [state, setState] = useState<LoadState>('loading');
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [wsConnected, setWsConnected] = useState(false);
    const [wsReconnecting, setWsReconnecting] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimer = useRef<number | null>(null);

    const fetchCounts = useCallback(async (jobId: number | null) => {
        setState('loading');
        setErrorMessage('');
        try {
            const query = jobId ? `?job_id=${jobId}` : '';
            const response = await core.server.request('GET', `/test/tasks/${taskId}/annotation-counts${query}`);
            const data = response as CountsResponse;
            setPayload(data);
            setState(data.counts.length ? 'ready' : 'empty');
        } catch (error: unknown) {
            setPayload(null);
            setState('error');
            setErrorMessage(error instanceof Error ? error.message : 'Request failed');
        }
    }, [taskId]);

    const connectWebSocket = useCallback(() => {
        if (!Number.isInteger(taskId)) {
            return;
        }

        if (wsRef.current) {
            wsRef.current.close();
        }

        const socket = new WebSocket(wsUrl(taskId));
        wsRef.current = socket;

        socket.onopen = () => {
            setWsConnected(true);
            setWsReconnecting(false);
        };

        socket.onmessage = () => {
            void fetchCounts(jobFilter);
        };

        socket.onclose = () => {
            setWsConnected(false);
            setWsReconnecting(true);
            if (reconnectTimer.current) {
                window.clearTimeout(reconnectTimer.current);
            }
            reconnectTimer.current = window.setTimeout(() => {
                connectWebSocket();
            }, 3000);
        };

        socket.onerror = () => {
            socket.close();
        };
    }, [fetchCounts, jobFilter, taskId]);

    useEffect(() => {
        if (Number.isInteger(taskId)) {
            void fetchCounts(jobFilter);
            connectWebSocket();
        }
        return () => {
            if (reconnectTimer.current) {
                window.clearTimeout(reconnectTimer.current);
            }
            wsRef.current?.close();
        };
    }, [taskId, jobFilter, fetchCounts, connectWebSocket]);

    const chartData = useMemo(() => {
        const labels = payload?.counts.map((row) => row.label) ?? [];
        const values = payload?.counts.map((row) => row.count) ?? [];
        return {
            labels,
            datasets: [{
                label: 'Annotations',
                data: values,
                backgroundColor: 'rgba(24, 144, 255, 0.65)',
            }],
        };
    }, [payload]);

    if (!Number.isInteger(taskId)) {
        return <Result status='404' title='Invalid task id' />;
    }

    return (
        <div className='cvat-class-analytics-page'>
            <Row justify='center'>
                <Col span={22} xl={18} xxl={14}>
                    <GoBackButton />
                    <Typography.Title level={3} className='cvat-class-analytics-title'>
                        Class annotation analytics
                    </Typography.Title>
                    <Typography.Paragraph type='secondary'>
                        Task #{taskId}
                        {' · '}
                        {wsConnected ? 'Live (WebSocket)' : wsReconnecting ? 'Reconnecting…' : 'Offline'}
                    </Typography.Paragraph>
                    <div className='cvat-class-analytics-filters'>
                        <Typography.Text>Filter by job ID (optional):</Typography.Text>
                        <InputNumber
                            min={1}
                            placeholder='All jobs'
                            value={jobFilter ?? undefined}
                            onChange={(value) => setJobFilter(typeof value === 'number' ? value : null)}
                        />
                    </div>
                    {state === 'loading' && <Spin size='large' />}
                    {state === 'error' && (
                        <Alert
                            type='error'
                            showIcon
                            message='Could not load annotation counts'
                            description={errorMessage}
                        />
                    )}
                    {state === 'empty' && (
                        <Empty description='No annotations for this task (or filter).' />
                    )}
                    {state === 'ready' && payload && (
                        <div className='cvat-class-analytics-chart'>
                            <Bar
                                data={chartData}
                                options={{
                                    responsive: true,
                                    plugins: {
                                        legend: { display: false },
                                        title: { display: true, text: 'Annotations per class' },
                                    },
                                }}
                            />
                        </div>
                    )}
                </Col>
            </Row>
        </div>
    );
}

export default ClassAnalyticsPage;
