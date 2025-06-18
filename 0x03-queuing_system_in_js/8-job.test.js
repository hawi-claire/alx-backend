#!/usr/bin/yarn test
import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue({ testMode: true });

describe('createPushNotificationsJobs', () => {
  before(() => queue.testMode.enter());
  afterEach(() => queue.testMode.clear());
  after(() => queue.testMode.exit());

  it('display a error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '123', message: 'Hello' },
      { phoneNumber: '456', message: 'World' },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });
});
